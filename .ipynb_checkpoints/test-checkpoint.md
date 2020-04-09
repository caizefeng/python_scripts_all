## MOOC笔记

### VASP课程

#### DFT催化应用

1. 催化剂本身性质
    1) 催化剂电子结构（DOS等）
    2) 几何结构及其对催化剂性质的影响（不同结构（shell-core/random等）能量稳定性）
    3) 催化剂费米性质偏移和纳米结构的关系（nanoisland/nanobar等）

2. 与反应物的相互作用
    1) 电荷密度变化（吸附电荷转移）
    2) 电子结构与成键情况（不同表面催化加氢，H的成键反键轨道在DOS上的位置）
    3) 相关能量变化以及振动频率对比（实验通过红外谱确定吸附位）

3. 反应过程的计算
    1. 过渡态搜索（不同催化剂）
    2. 电化学反应过程（不同电极材料free energy垒）
    3. 反应历程PH变化

**Note**:计算参数尽量从已有文献出发，避免大量收敛性测试和验证。

**计算对象及意义：**

1. 结构信息
    1. 确定稳定结构
    2. 确定键长键角
    3. 确定晶格常数、
    4. 确定形貌（与TEM/EXAFS对比）

2. Stability

Alloy System: excess energy  
$$
E_{exc} = (1/N) \times (E_{AB}-n_A/N*E_{bulkA}-n_B/N*E_{bulkB}) \\
N = n_A+n_B
$$
    
Cluster: cohesive energy
$$
E_{cohesive} = (-)(1/n)*(E_{An}-n*E_A(single\ atom))
$$
Adsorption/Doping Structure:binding energy
$$
E_b = -(E_{A+B}-n_A*E_A-E_{bulkB})/n
$$
$n_A$ is the number of atoms adsorped/doped in calculated model
n is the total number of atoms in the model

Adsorption: adsorption energy  
$$
E_{ad} = (E_{total} - E_{slab} -E_{adsorbant})/A
$$
A is the area of the surface model


metal(cluster)-substrate: adhesive energy
$$
E_A = E_b-E_{cohesive}
$$
(only calculated the potential energy induced by surfacial interaction)  
not necessary

Vacancy formation: formation energy  
$$
E_{formation} = E_{A-van} + E_A - E_{no-van}
$$
$E_{A-van}$:具A空位的模型能量  
$E_{no-van}$:完整不具空位的模型能量  
$E_A$:空位原子能量  

Surface: surface energy
1) 判断主要暴露面  
2) 选取稳定表面 √  
3) 选取稳定终端层  
$$
\gamma = (E_{slab}-n(E_{A-in-bulk}))/2A
$$
3. Frequency 
    1. 判断结构稳定性（虚频不稳定）
    2. 判断过渡态（过渡态总在虚频处）
    3. 对比FTIR数据（如判断吸附位，吸附质在不同吸附位红外谱位置不同）
    4. Raman数据
    5. 计算热力学性质（熵、热容）  
**Note**：能量稳定不一定是真正的吸附位，fcc吸附能大于top吸附，但CO在一些表面上的吸附却是以top为主。	 

4. Charge Distribution (or difference charge distribution)
    1. 解释XPS偏移（X射线光电子能谱）
    2. 解释催化活性
    3. 解释反应物（吸附物）活化
    4. 解释轨道杂化。

5. Electron locallization function(ELF)  
chemical bonding classification(sigma bonding/pi bonding...)

6. HOMO 轨道图  
    1. 确认bonding states（sigma/pi/omega）
    2. orbital hybridization （back-donation等）
    3. activation parts （活性位点）

7. DOS
    1. electronic structure
    2. bonding states
    3. band gap
    4. band center（如过渡金属d带中心决定解离能）  
**Note**：和催化剂类型有关，非过渡金属催化剂如In通过s-p杂化催化CO2还原反应。此时p带中心更为重要。
    5. 催化性能

8. Band Structure 

9. 过渡态搜索  
    1. 确认反应路径机理
    2. 确认活化能
    3. 计算反应速率常数

10. TOF(Turnover frequency)  
解释催化剂性能
如氨合成第一步N2 dissociation energy和N2 transition state energy为坐标的TOFcontour图。

11. Gibbs free Energy  
评价电化学反应催化剂性能，探索电化学反应机理（如燃料电池O2反应，Pt电极在第一步加氢时没有能垒，所以使用广泛）

12. Potential-pH diagram  
不同pH下的电极电势

delta_G = delta_E(DFT energy) - T*delta_S + delta_ZPE + n(参与电子数)*e*(U-U0)

---
### MD（LAMMPS）课程

LJ不是Morse的特例。

二体势空位能恒等于内聚能。

在内层循环中将一个原子根据PBC分化成多个原子镜像，利用系统合势能公式计算一个周期性单元中
所有原子的合势能，仍然是正确的。只是因为引入r\_c时，r\_c一般小于任一周期性单元边长一半，分化成的多个镜像只有一个有效用。

实空间级数不收敛的远程势（如1/r）Fourier变换到倒空间，将其中有限项相加。

任意体系，平均动能恒等于3/2T

另一种角度：MD是不能获得解析解问题的一种数值积分方法

收敛速度： steepest descent \> CG \> Newton

缺陷形成能（defect formation energy) 恒等于缺陷体系能量减对应完美体系能量

从收敛体系开始静态性质计算有计算成本上的优势。

Note: 绝大多数静态计算都不会到达global minimum

表面能常用单位 J/m^2

ovito 的 “import remote files" 功能会缓存相同地址同名文件，所以文件有更改需改名再import

温度越高 时间步应取得越小

---
### DeepMD-kit workshop

uncontroled approximation (e.g. DFT)  
controled approximation

OFSFT orbital-free dft

DFT用于产生训练数据的问题：
赝势方法在辐照问题等原子间距小于赝势截断半径时缺乏物理意义，全电子近似则计算过于昂贵，对于应用目的得不偿失；另外不含时DFT结果具有局限性，仅用DFT结果训练用于辐照问题相当于采用BO近似，得到的势函数物理上效果不会好，ZBL等经验力场反而更准确。含时DFT则也具有运算过于昂贵的问题。